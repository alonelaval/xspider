#!usr/bin/env python
# -*- coding:utf-8 -*-
# Create on 2017.2.21

import os
import hashlib
import traceback
from django.conf import settings

# Database Models
from collector.models import Project, Task, Result


class InitSpider(object):
    """
    Load Spider Script to Local File
    """

    def __init__(self):
        """
        LoadSpider Initialization
        """
        if not os.path.exists(settings.EXECUTE_PATH):
            os.mkdir(settings.EXECUTE_PATH)

    def load_spider(self, project):
        """
        Load Spider from  Database by project
        :param project:
        :return:
        """
        try:
            project = Project.objects().first()
            project_name = project.name
            spider_script = project.script
            models_script = project.models
            _spider_path = os.path.join(settings.EXECUTE_PATH, "%s_spider.py" %(project_name))
            _models_path = os.path.join(settings.EXECUTE_PATH, "%s_models.py" %(project_name))
            execute_init = os.path.join(settings.EXECUTE_PATH, "__init__.py")

            with open(execute_init, 'w') as fp:
                fp.write("")
            with open(_spider_path, 'w') as fp:
                fp.write(spider_script.encode('utf8'))
            with open(_models_path, 'w') as fp:
                fp.write(models_script.encode('utf8'))

        except Exception:
            print traceback.format_exc()


class Generator(object):
    """
    Generator Module
    """

    def __init__(self, project):
        """
        Generator Module Initialization
        """

        self.project = project
        InitSpider().load_spider(self.project)

    def generate_task(self):
        """
        Execute Spider Generator Tasks
        :return: URL List
        :example: [{"url":"http://www.example.com","args":None}]
        """
        project_name = self.project.name
        _generator = __import__("execute.{0}_spider".format(project_name), fromlist=["*"])
        spider_generator = _generator.Generator()
        result = spider_generator.start_generator()

        return result

    def save_task(self, result):
        """
        Save Generator Result to Task Database
        :param result:
        :return:
        """
        if not isinstance(result, list):
            raise TypeError("Generator Result Must Be List Type.")

        for url_dict in result:
            if not isinstance(url_dict, dict):
                raise TypeError(("Generator URL Result Must Be Dict Type."))

            if self.project.status == 1:
                # Save Task to Database
                # TODO
                return url_dict

            elif self.project.status == 2:
                # Create Debug Task Object && Dynamic Import Models
                exec("from execute.{0}_models import *".format(self.project.name))
                exec("task_object = {0}{1}()".format(str(self.project.name).capitalize(), "Task"))

                url = url_dict.get("url")
                task_id = self.str2md5(url_dict.get("url"))

                task_object.project = self.project
                task_object.task_id = task_id
                task_object.status = 0
                task_object.url = url

                return task_object
            else:
                return url_dict

    @staticmethod
    def str2md5(string):
        """
        Convert Str to MD5
        :return:
        """
        md5 = hashlib.md5()
        md5.update(string)

        return md5.hexdigest()

    def run_generator(self):
        """
        Run Generator
        :return:
        """
        result = self.generate_task()
        result = self.save_task(result)
        return result


class Processor(object):
    """
     Processor Module
    """
    def __init__(self, task):
        """
        Processor Module Initialization
        :param object:
        """
        self.task = task

    def process_task(self):
        """
        Downloader Module
        :return: Result Dict
        """
        try:
            task_url = self.task.url
            args = self.task.args

            project_name = self.task.project.name
            _spider = __import__("execute.{0}_spider".format(project_name), fromlist=["*"])
            _downloader = _spider.Downloader()
            _parser = _spider.Parser()

            resp = _downloader.start_downloader(task_url, args)
            result = _parser.start_parser(resp)

            print result
            # record log

        except Exception:
            print traceback.format_exc()
            # record log