# lovefreshbee
纪念程序员生涯中第一个项目
后续我会补上一些文档，可以协作开发练习一个项目

Tips: checkout the [API Documentation](https://github.com/brother-fans/lfb_backend/wiki) first

Any questions? Contact awesome devs!

- 1258040085@qq.com

---

- [lfb_backend](#lovefreshbee)

  - [Installation](#installation)
  - [Run](#run)
    - [Local Dev](#local-dev)
    - [Development](#development)
    - [Test](#test)
    - [Production](#Production)
  - [Project Structure](#project-structure)
  - [Tests](#tests)
    - [Unit Test](#unit-test)
    - [Functional Test](#functional-test)
    - [Integration Test](#integration-test)
  - [Supporting Team](#supporting-team)

  

## Installation

**Python Version:3.5+**

```bash
$ pip install -r requirements.txt
```

## Run

### Local Dev

```bash
$ python lfb_backend/manage.py runserver --settings=config.settings.local
```

if you have your own config script

 ```bash
$ touch lfb_backend/config/settings/local_{yourinitials}.py

# create your own config file

$ vim lfb_backend/config/settings/local_{yourinitials}.py

# add your own configs

$ python lfb_backend/manage.py runserver --settings=config.settings.local_{yourinitials}
 ```

### Development

```bash
$ python lfb_backend/manage.py runserver --settings=config.settings.dev 
```

### Test

```bash
$ python lfb_backend/manage.py runserver --settings=config.settings.test
```

### Production

```bash
$ python lfb_backend/manage.py runserver --settings=config.settings.prod
```

## Project Structure

## Tests

### Unit Test

### Functional Test

### Integration Test

## Supporting Team

- cjl 1258040085@qq.com
- zy
- yhc
- lyb
- fjj
- wqm