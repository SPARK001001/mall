FROM    bbbenpjr/jdk1.8u181:1.0
MAINTAINER     "jianrongpeng@sohu-inc.com"
COPY mall-admin.jar /home/project/mall-admin.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/home/project/mall-admin.jar"]