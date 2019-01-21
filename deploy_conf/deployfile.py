# coding=utf-8
from __future__ import with_statement
from fabric.api import *
import time
def deploy(project_name,sub_project_name):
    base_path = '/home/data/project/%s'

    version = time.strftime("%Y%m%d%H%M%S", time.localtime())
    with lcd(base_path % project_name):
        # 更新代码
        local('git pull')
        # 打包
        local('mvn package')

        local('cp %s/target/%s.jar deploy_conf/' % (sub_project_name,sub_project_name))
        # build 镜像
        local('sudo docker build deploy_conf/ -t bbbenpjr/%s:%s' % (
            sub_project_name, version))
        local('sudo docker push bbbenpjr/%s:%s' % (sub_project_name, version))
        # 重写配置文件
        rewrite_yaml('%s/deploy_conf/' % (base_path % project_name,), '%s:%s' % (sub_project_name, version))
        # k8s 部署
        local('kubectl apply -f deploy_conf/k8s_deploy.yaml --record')
        # # nginx reload
        # local('cp deploy_conf/nginx.conf /home/data/nginx-conf/%s.conf' % (project_name,))
        # local('sudo nginx -s reload')
def rewrite_yaml(file_path, image_name):
    """
    读取 deploy.yaml、覆盖 {image}，保存为 k8s_deploy.yaml
    :param file_path:
    :param image_name:
    :return:
    """
    with open(file_path + 'deploy.yaml', 'r') as f:
        data = f.read()
        new_data = data.replace('{image}', image_name)
        #print new_data
    with open(file_path + 'k8s_deploy.yaml', 'w') as f:
        f.write(new_data)

deploy('mall','mall-admin')

