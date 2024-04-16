# SaleWeb
本项目后端应用Django，前端三件卡应用Bootstrap和Echarts美化绘制图表，数据部署在Hadoop上，利用Hive进行分布式数据分析。数据为用faker制造的数据

## 大数据部署
hadoop hive首先从官网下载源程序包解压，流程可上网查询。

hadoop部署主要通过./etc/hadoop/文件夹中的配置,下面是我的一些配置。各种坑基本都是配置问题。这里通过单机模拟分布式。

```txt
### vim core-site
<configuration>
 <property>
 <name>hadoop.tmp.dir</name>

 <value>file:/usr/local/hadoop/tmp</value>
 <description>Abase for other temporary directories.</description>
 </property>
 <property>
 <name>fs.defaultFS</name>
 <value>hdfs://localhost:9000</value>
 </property>
         <property>
        <name>hadoop.proxyuser.root.hosts</name>
        <value>*</value>
</property>
<property>
        <name>hadoop.proxyuser.root.groups</name>
        <value>*</value>
</property>
### vim hdfs-site.xml 
</configuration>

<configuration>
<property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/data</value>
</property>
        <property>
          <name>dfs.http.address</name>
          <value>0.0.0.0:50070</value>
    </property>
</configuration>

#其他如yarn-env.xml/mapred-site.xml等都可以网上寻找配置
```
中间的坑：
找不到JAVA_HOME,注意hadoop-env.sh中间java_home写绝对路径！

部署后通过jps指令查看，正常应该有主节点和分节点，另外还应该有yarn控制节点，也就是manager节点。
```txt
test@test:~/SaleWeb$ jps
354854 SecondaryNameNode
491088 NodeManager
490527 ResourceManager
485917 RunJar
335866 NameNode
657557 Jps
337562 DataNode
```
后面部署hive，hive需要在conf文件夹中配置hive-site.xml,非常重要的部分，坑都可以查看这个部分配置。
```txt
<configuration>
<property>
    <name>hive.metastore.schema.verification</name>
    <value>false</value>
     <description>
          Enforce metastore schema version consistency.
          True: Verify that version information stored in metastore matches with one from Hive jars.  Also disable automatic
          schema migration attempt. Users are required to manully migrate schema after Hive upgrade which ensures
          proper metastore schema migration. (Default)
          False: Warn if the version information stored in metastore doesn't match with one from in Hive jars.
      </description>
    </property>
    <!-- 存储在hdfs上的数据路径 -->
    <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/user/hive/warehouse</value>
    <description>location of default database for the warehouse</description>
  </property>
  <property>
    <name>hive.exec.scratchdir</name>
    <value>/tmp/hive</value>
    <description>HDFS root scratch dir for Hive jobs which gets created with write all (733) permission. For each connecting user, an HDFS scratch dir: ${hive.exec.scratchdir}/&lt;username&gt; is created, with ${hive.scratch.dir.permission}.</description>
  </property>

        <property>
    <name>hive.exec.mode.local.auto</name>
    <value>true</value>
</property>
  <property>
  <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true&amp;useSSL=false&amp;allowPublicKeyRetrieval=true</value>
    <description>JDBC connect string for a JDBC metastore</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>com.mysql.cj.jdbc.Driver</value>
    <description>Driver class name for a JDBC metastore</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hive</value>
    <description>username to use against metastore database</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>hive</value>
    <description>password to use against metastore database</description>
  </property>
  </property>
## 定义hiveserver2的端口
  <property>
<name>hive.server2.thrift.port</name>
<value>10000</value>
<description>Port number of HiveServer2 Thrift interface when hive.server2.transport.mode is 'binary'.</description>

## 这个配置防止出现pyhive或者其他调用方式调用hiveserver2出现无法建立session的bug
</property>
        <property>
  <name>hive.server2.enable.doAs</name>
  <value>false</value>
  </property>
</configuration>
```

在配置文件后，还需要将mysql-connector-java-8.0.11.jar
或者mysql-connector-java-5.1.49.jar放入lib文件夹中，注意配置中的com.mysql.cj.jdbc.Driver对应8版本，而com.mysql.jdbc.Driver对应5版本，具体可上网查询。

根据原理，hive在hdfs数据存储的元数据表存放在mysql的指定databases中，这个databases可能在之前配置与报错中产生大量数据，若一直报错找不到问题，可以看指定的mysql元表是不是有内容了，可以删除表，重新生成新的表。本配置中的元数据表是hive用户，密码为hive，可见配置信息中相应信息。
验证hive部署成功可以命令行hive，执行show databases;正常是没有报错的返回ok。

后续项目中可通过pyhive调用hive，完成后端数据crud。