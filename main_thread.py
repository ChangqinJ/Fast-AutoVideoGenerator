from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable
import pymysql
from pymysql.cursors import DictCursor
from DBpool import DBpool
from queue import Queue
import simple_log
import time
import read_config

# 在使用游标进行操作时, 添加重试机制, 自定义重试次数(3~5次)
# 弹出特定异常, 即触发重试, 其他异常不触发重试

def retry(conn:pymysql.Connection,max_retry_times:int=5):
  status = False
  for i in range(max_retry_times):
    try:
      conn.ping(reconnect=True)
    except pymysql.err.OperationalError as errOpt:
      print(f'OperationalError {errOpt}! Retry failed, retrying times: {i}')
      time.sleep(1)
    except pymysql.err.Error as err:
      print(f'MySQL Error {err}! Retry failed, retrying times: {i}')
      time.sleep(1)
    except Exception as e:
      print(f'Unknown exception {e}! Retry failed, retrying times: {i}')
      time.sleep(1)
    else:
      status = True
      break
  return status

def retry_execute(cursor:DictCursor,logging_path:str,sql:str,args:tuple=None,max_retry_times:int=5):
  status = False
  for i in range(max_retry_times):
    try:
      cursor.execute(sql,args) #执行弹出异常
    except (pymysql.err.InterfaceError,pymysql.err.OperationalError) as e:
      if e.args[0] in (0,2003,2006,2013):
        if retry(cursor.connection,max_retry_times=max_retry_times) == True:
          #连接异常且重试成功
          simple_log.log(f'Retry success, retrying times: {i}\nIn main_thread.retry_execute',log_path=logging_path)
          continue
        else:
          simple_log.log(f'Retry failed, error:{e}, retrying times: {i}\nIn main_thread.retry_execute',log_path=logging_path)
          continue
      else:
        simple_log.log(f"Exception {e}! Retry failed, retrying times: {i}\nIn main_thread.retry_execute",log_path=logging_path)
        continue
    except Exception as e:
      simple_log.log(f'Other exception {e}! Retry failed, retrying times: {i}\nIn main_thread.retry_execute',log_path=logging_path)
      continue
    else:
      status = True
      break
  return status

class main_thread:
  # 连接测试成功
  def __init__(self,func:Callable,host:str='testapi.fuhu.tech',port:int=3306,user:str='ai_creator',password:str='ai_creator123456',db:str='esports',max_connections:int=10, logging_path:str='./logging_dir', max_retry_times:int=5):
    '''
    func: 接收字典和线程池引用作为参数, 返回tuple[int,None|str]
    host: 数据库主机
    port: 数据库端口
    user: 数据库用户
    password: 数据库密码
    db: 数据库名称
    max_connections: 数据库连接池最大连接数(近似认为是数据库访问的并行程度)
    '''
    self.func = func
    self.host = host
    self.port = port
    self.user = user
    self.password = password
    self.db = db
    self.queue = Queue()
    self.status=True
    self.dbpool = DBpool(max_connections=max_connections,host=host,port=port,user=user,password=password,db=db,cursorclass='DictCursor')
    self.logging_path = logging_path
    self.max_retry_times=max_retry_times
    try:
      self.conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db,cursorclass=DictCursor,autocommit=False)
      self.dbpool.put_connection(self.conn)
    except pymysql.Error as e:
      self.dbpool.close()
      simple_log.log(str(e),log_path=self.logging_path)
      raise e
  
  def init_process(self,max_workers:int=10):
    pass
  
  def fetch_status0(self,ub:int=10):
    '''
    从数据库中找到特定数量的state=0的记录并添加到queue中, 并更新state为1
    '''
    rows = []
    conn = None
    cursor = None
    try:
      # 每次获取新的连接，避免事务状态问题
      conn = self.dbpool.get_connection()
      cursor = conn.cursor()
      
      # 设置事务隔离级别为READ COMMITTED，确保能看到其他事务已提交的数据
      cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
      
      #弱点: 不熟悉数据库的事务和锁机制
      
      # 使用原子操作：先更新再查询，避免竞态条件
      # 使用FOR UPDATE SKIP LOCKED来避免锁定冲突
      sql = '''
      SELECT * FROM movie_agent_tasks 
      WHERE state = 0 
      ORDER BY id 
      LIMIT %s 
      FOR UPDATE SKIP LOCKED
      '''
      args = (ub,)
      
      status = retry_execute(cursor, self.logging_path, sql, args, self.max_retry_times)
      if status == False:
        raise Exception('Error in fetch_status0:retry_execute(sql,args) for finding rows with state=0')
      
      rows = list(cursor.fetchall())
      print('--------------------------------------------------------rows size:',len(rows))
      
      if len(rows) > 0:
        # 立即更新这些记录的状态为1
        placeholders = ','.join(['%s'] * len(rows))
        sql = f'UPDATE movie_agent_tasks SET state = 1 WHERE id IN ({placeholders})'
        args = tuple(row['id'] for row in rows)
        
        res = retry_execute(cursor, self.logging_path, sql, args, self.max_retry_times)
        if res == False:
          conn.rollback()
          raise Exception("Retry failed, error in fetch_status0:retry_execute(sql,args), update state to 1")
        else:
          conn.commit()
          simple_log.log(f'Successfully updated {len(rows)} tasks from state=0 to state=1', log_path=self.logging_path)
          
      else: #测试语句, 正式调试时删除
        print('no rows to update')
        time.sleep(5)
      
      idlist = []
      if len(rows) > 0:
        for row in rows:
          self.queue.put(row)
          idlist.append(row['id'])
      
      return idlist
      
    except Exception as e:
      simple_log.log(f'Error in fetch_status0: {str(e)}', log_path=self.logging_path)
      if conn:
        try:
          conn.rollback()
        except:
          pass
      raise e
    finally:
      if cursor:
        try:
          cursor.close()
        except:
          pass
      if conn:
        try:
          self.dbpool.put_connection(conn)
        except:
          pass
      
  #测试成功
  def close(self):
    self.dbpool.close()
  
  class callback:
    def __init__(self,package:dict[str,any],dbpool:DBpool,logging_path:str,max_retry_times:int = 5):
      self.package=package
      self.dbpool=dbpool
      self.logging_path=logging_path
      self.max_retry_times=max_retry_times
    def __call__(self,future:Future[tuple[int,None|str]]):
      # 添加调试日志，确认回调函数被调用
      simple_log.log(f'Callback started for task {self.package["id"]}', log_path=self.logging_path)
      
      conn = None
      cursor = None
      try:
        # 检查Future状态
        if future.cancelled():
          simple_log.log(f'Task {self.package["id"]} was cancelled', log_path=self.logging_path)
          return
        
        conn = self.dbpool.get_connection()
        simple_log.log(f'Got database connection for task {self.package["id"]}', log_path=self.logging_path)
        
        # 获取任务结果
        result = future.result(timeout=30)  # 设置超时
        simple_log.log(f'Got result for task {self.package["id"]}: {result}', log_path=self.logging_path)
        
        # 处理结果
        index = result[0] #返回任务id
        msg = result[1] #返回错误信息, 在没有错误时, 信息为None
        state = 2 if msg is None else 3
        
        # 更新数据库
        sql = 'update movie_agent_tasks set state = %s, progress = 100 where id = %s'
        args = (state, index)
        
        cursor = conn.cursor()
        res = retry_execute(cursor, self.logging_path, sql, args, self.max_retry_times)
        
        if res == False:
          conn.rollback()
          raise Exception('Error in callback:retry_execute(sql,args) for updating state to 2 or 3')
        else:
          conn.commit()
          simple_log.log(f'Successfully updated task {self.package["id"]} state to {state}', log_path=self.logging_path)
          
      except Exception as e:
        simple_log.log(f'Exception in callback for task {self.package["id"]}: {str(e)}', log_path=self.logging_path)
        if conn:
          try:
            conn.rollback()
          except:
            pass
        # 不要重新抛出异常，避免影响其他回调
      finally:
        if cursor:
          try:
            cursor.close()
          except:
            pass
        if conn:
          try:
            self.dbpool.put_connection(conn)
          except:
            pass
        simple_log.log(f'Callback completed for task {self.package["id"]}', log_path=self.logging_path)
  
  def add_output_path(self,args:dict[str,any]):
    pass
  
  def run(self, slice_size:int=10,max_workers:int=10):
    '''
    查找数据库中status为0的记录, 每一条记录都开一个线程处理, 线程数不够则等待
    '''
    try:
      with ThreadPoolExecutor(max_workers=max_workers) as executor:
        times = 0 #测试语句, 正式调试时删除
        while True:
          self.init_process(max_workers=max_workers) #初始化进程, 在最新版本main_thread_cfg_init中, 函数依照is_init值决定是否执行, 并保证在服务器开启后只执行一次
          print('times:',times) #测试语句, 正式调试时删除
          times += 1 #测试语句, 正式调试时删除
          if self.status == False:
            break
          print('before fetch_status0, times:',times) #测试语句, 正式调试时删除
          idlist = self.fetch_status0(slice_size) #每次获取10条数据, 进行测试, 正式调试传入1024
          
          #捕获数据后, 返回全部行数据的id, 用于更新进度条
          print('idlist:',idlist) #测试语句, 正式调试时删除
          if self.queue.empty():
            print('queue is empty, times:',times) #测试语句, 正式调试时删除
          
          print('after fetch_status0, times:',times) #测试语句, 正式调试时删除
          futures = []  # 存储所有的Future对象
          while not self.queue.empty():
            print('into cycle, times:',times) #测试语句, 正式调试时删除
            '''
            对queue中的每一行, 开一个线程处理
            在处理结束后将queue中的行状态改为2
            '''
            
            '''
            self.func接收参数为字典, 字典内容为{'id','task_uuid','prompt','width','height'}
            '''
            row = self.queue.get()
            args = {'id':row['id'],'task_uuid':row['task_uuid'],'prompt':row['prompt'],'width':row['width'],'height':row['height'],'movie_agent_pack_id':row['movie_agent_pack_id']}
            # ,'movie_agent_pack_id':row['movie_agent_pack_id']
            self.add_output_path(args)
            
            # 提交任务到线程池
            future = executor.submit(self.func,args,self.dbpool)
            futures.append(future)  # 保存Future对象
            
            # 添加回调函数
            callback_obj = main_thread.callback(args,self.dbpool,self.logging_path)
            future.add_done_callback(callback_obj)
            
            simple_log.log(f'Submitted task {args["id"]} to thread pool', log_path=self.logging_path)
          
          # 等待所有任务完成（可选，用于调试）
          if futures:
            simple_log.log(f'Waiting for {len(futures)} tasks to complete', log_path=self.logging_path)
            # 注意：这里不等待完成，让任务在后台运行
            # 如果需要等待，可以取消注释下面这行
            # executor.shutdown(wait=True)
          print('queue size:',self.queue.qsize()) #测试语句, 正式调试时删除
    finally:
      self.close()

class main_thread_with_config(main_thread):
  def __init__(self,func:Callable,path_config:str):
    '''
    传入config.json文件路径, 读取配置文件, 并初始化main_thread
    '''
    self.path_config = path_config
    self.config = read_config.read_config(path_config)
    if self.config is None:
      raise RuntimeError('Failed to load config')
    super().__init__(func=func,host=self.config['host'],port=self.config['port'],user=self.config['user'],password=self.config['password'],db=self.config['db'],max_connections=self.config['max_connections'],logging_path=self.config['log_path'],max_retry_times=self.config['max_retry_times'])
    self.output_path = self.config['output_path']
    # 测试语句, 正式调试时删除
    print('path_config: ',path_config)
    print('config: ',self.config)
    print('max_retry_times: ',self.config['max_retry_times'])
    
  def add_output_path(self,args:dict[str,any]):
    args['output_path'] = self.output_path

class main_thread_cfg_init(main_thread_with_config):
  def __init__(self,func:Callable,path_config:str):
    self.__is_init = True
    super().__init__(func=func,path_config=path_config)
  
  #确实可以在开始时将全部未完成任务状态转回为0, 但是无法保证在run过程中不会出现新的未完成任务
  def init_process(self,max_workers:int=10):
    '''
    在服务器启动时, 只负责将未完成任务的状态转回为0, 接下来交给run处理
    本函数只在初始状态执行一次
    '''
    if self.__is_init == False:
      return
    else:
      print('start init_process')
      self.__is_init = False
      conn = self.dbpool.get_connection()
      try:
        with conn.cursor() as cursor:
          #测试语句 - 查看更新前的状态
          sql = 'select id from movie_agent_tasks where state = 1'
          res=retry_execute(cursor,self.logging_path,sql,None,self.max_retry_times)
          print('res:',res)
          if res == False:
            raise Exception('Error in init_process:retry_execute(sql,args) for finding rows with state=1')
          
          state_1_ids = [row['id'] for row in cursor.fetchall()]
          print('\nstate_1_ids size:\n',len(state_1_ids),'\nstate_1_ids:\n',state_1_ids)
          print('**************************************************************************')
          # update语句中最好不要嵌套子查询, 否则会报错
          if len(state_1_ids) > 0:
            # 使用IN子句进行更新
            placeholders = ','.join(['%s'] * len(state_1_ids))
            sql = f'update movie_agent_tasks set state = 0 where id in ({placeholders})'
            args = tuple(state_1_ids)
            res = retry_execute(cursor,self.logging_path,sql,args,self.max_retry_times)
            conn.commit()
            print('res:',res)
            if res == False:
              conn.rollback()
              print('Error in init_process:retry_execute(sql,args) for updating state to 0')
              raise Exception('Error in init_process:retry_execute(sql,args) for updating state to 0')
            affected_rows = cursor.rowcount
            print(f'update success, affected rows: {affected_rows}')
          else:
            print('no rows with state=1 to update')
          
          #测试语句 - 查看更新后的状态
          test_list = []
          sql = 'select id from movie_agent_tasks where state = 1'
          res = retry_execute(cursor,self.logging_path,sql,None,self.max_retry_times)
          if res == False:
            raise Exception('Error in init_process:retry_execute(sql,args) for finding rows with state=1')
          else:
            test_list = list(cursor.fetchall())
          print('test_list: (after update)\n',test_list)
          
      except Exception as e:
        print(f'init_process failed: {str(e)}')
        simple_log.log(str(e)+' init_process failed',log_path=self.logging_path)
      finally:
        self.dbpool.put_connection(conn)
    print('end init_process')