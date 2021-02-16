# agile-test-data-platform

A fully asynchronous scripting framework for the build process in agile testing, serving as a platform for development and testing, all based on coroutines.
That is (Ayncio).

这是一个全异步的脚本框架，用于敏捷测试中的造数过程，服务于开发和测试的一个平台，全部基于协程完成。
即（ayncio）。

## Docker
```shell
docker build -t atdp .
```

## Usage

```shell
➜  agile-test-data-platform git:(main) python3 cli.py
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --mysql_host TEXT     Mysql connect host
  --mysql_port INTEGER  Mysql connect port
  --mysql_user TEXT     Mysql connect user
  --mysql_passwd TEXT   Mysql connect passwd
  --help                Show this message and exit.

Commands:
  execute  执行造数
  init-db  初始化数据库
```

## 初始化数据库

```
python3 cli.py init-db
```

## 执行造数

```
python3 cli.py execute --table "my.runoob_tbl"  --uniq_key "runoob_id=1" --task_name "测试"
```

## 过程演示

```
mysql> show create table my.runoob_tbl\G
*************************** 1. row ***************************
       Table: runoob_tbl
Create Table: CREATE TABLE `runoob_tbl` (
  `runoob_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `runoob_title` varchar(100) NOT NULL,
  `runoob_author` varchar(40) NOT NULL,
  `submission_date` date DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  PRIMARY KEY (`runoob_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)

mysql> select * from my.runoob_tbl;
+-----------+--------------+---------------+-----------------+------+
| runoob_id | runoob_title | runoob_author | submission_date | type |
+-----------+--------------+---------------+-----------------+------+
|         1 |  PHP         |               | 2021-02-14      |    1 |
|         2 |  MySQL       |               | 2021-02-14      |    1 |
|         3 | JAVA         | RUNOOB.COM    | 2016-05-06      |    2 |
+-----------+--------------+---------------+-----------------+------+

mysql> select * from `atdp`.`tasks`;
Empty set (0.00 sec)

mysql> select * from `atdp`.`entries`;
Empty set (0.00 sec)

```

### 执行造数

```shell
➜  agile-test-data-platform git:(main) ✗ python3 cli.py execute --table "my.runoob_tbl"  --uniq_key "type=1" --task_name "开发测试"
2021-02-16 18:44:16,641[INFO]root:{config_manager.py:78}:Initialize [dev] config successfully
2021-02-16 18:44:16,641[INFO]root:{config_manager.py:30}:Set MYSQL infomation successfully : {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': '123456'}
2021-02-16 18:44:16,641[INFO]cmd:{execute.py:7}:Created Task(meta=Meta(table=my.runoob_tbl,uniq_key=['type=1']),scenario=Scenario(name=开发测试,identify=9c67a77b8d0a0872a0180654cd331bf4),sink_type=mysql,entries=[])
2021-02-16 18:44:16,645[DEBUG]domain:{context.py:35}:Initialize Context(mysql_pool={'min_size': 1, 'max_size': 10, 'loop': <_UnixSelectorEventLoop running=False closed=False debug=False>, 'echo': True, 'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': '123456'}) successfully
2021-02-16 18:44:16,646[DEBUG]domain:{sinker.py:86}:[ SELECT * FROM atdp.tasks WHERE `identify` = '9c67a77b8d0a0872a0180654cd331bf4' ]
2021-02-16 18:44:16,650[DEBUG]domain:{sinker.py:114}:[ SELECT * FROM my.runoob_tbl WHERE type=1 ]
2021-02-16 18:44:16,652[DEBUG]domain:{sinker.py:143}:[ INSERT INTO my.runoob_tbl (`runoob_id`,`runoob_title`,`runoob_author`,`submission_date`,`type`) VALUES (1," PHP","","2021-02-14",1),(2," MySQL","","2021-02-14",1) ]
```

### 查看最新数据

```
mysql> select * from `atdp`.`tasks`;
+----+----------------------------------+------+--------------------------+--------------+
| id | identify                         | name | identify_ref             | created_time |
+----+----------------------------------+------+--------------------------+--------------+
| 36 | 9c67a77b8d0a0872a0180654cd331bf4 | 开发测试 | my.runoob_tbltype=1mysql |   1613472256 |
+----+----------------------------------+------+--------------------------+--------------+
1 row in set (0.00 sec)

mysql> select * from `atdp`.`entries`;
+----+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id | task_id | sql                                                                                                                                                                |
+----+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  4 |      36 | INSERT INTO my.runoob_tbl (`runoob_id`,`runoob_title`,`runoob_author`,`submission_date`,`type`) VALUES (1," PHP","","2021-02-14",1),(2," MySQL","","2021-02-14",1) |
+----+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

