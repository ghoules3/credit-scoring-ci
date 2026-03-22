# Лабораторная работа 4 Автоматизация ETL/Scoring-скрипта с помощью CI/CD  
Бочков Андрей Александрович  
БД251-М Вариант 3  
**Предметная область:** Финансы    
**Компонент:** Scoring Model    
**Сценарий проверки:** unit-тестирование логики через `pytest`  
  
## Цель работы  
Настроить автоматический конвейер непрерывной интеграции (CI/CD) для кредитного скоринга.  
Обеспечить автоматическую:  
-проверку качества кода через unit-тесты  
-сборку Docker-образа  
-очистку ресурсов после завершения pipeline  
-демонстрацию провального и успешного сценариев  
  
## Выбранный подход  
Для выполнения лабораторной работы использован отдельный мини-проект `credit-scoring-ci`, развернутый в двух облачных CI/CD-платформах:  
-**GitVerse CI** для демонстрации инфраструктурных ограничений облачного раннера  
-**GitHub Actions** для успешного выполнения pipeline  
  
GitLab в данной работе не использовался.  
  
## Структура проекта  
```text  
credit_scoring_ci/  
  Dockerfile  
  requirements.txt  
  scoring_model.py  
  test_scoring.py  
  .github/  
    workflows/  
      github_pipeline.yml  
  gitverse/  
    workflows/  
      clean_up_pipeline.yaml  
  docs/
```
  
## Описание файлов  
`scoring_model.py`  
Содержит простую функцию оценки кредитного риска клиента:  
-`low`  
-`medium`  
-`high`  
  
Логика основана на трех входных параметрах:  
-`limit_bal`  
-`pay_delay`  
-`age`  
  
`test_scoring.py`    
Содержит unit-тесты для проверки scoring-логики.  
Всего реализовано 4 теста, покрывающих:  
-низкий риск  
-средний риск  
-высокий риск из-за низкого лимита  
-высокий риск из-за большой просрочки  
  
`requirements.txt`  
Минимальный набор зависимостей проекта:  
```text  
pytest==7.4.3
```
  
`Dockerfile`  
Описывает Docker-образ для запуска тестов в контейнере.  
Контейнер:  
-использует python:3.11-slim  
-устанавливает зависимости  
-копирует код проекта  
-запускает pytest  

## Локальная проверка  
Перед публикацией в облачные CI/CD-системы проект был проверен локально:  
### Проверка unit-тестов  
```Bash  
pytest -v
```
  
Результат:  
-найдено 4 теста  
-все тесты успешно пройдены  
  
### Сборка Docker-образа  
```Bash  
docker build -t credit-scoring-ci-test .
```
  
### Запуск контейнера с тестами  
```Bash   
docker run --rm credit-scoring-ci-test
```
  
Результат:  
-контейнер успешно запускается  
-тесты выполняются внутри контейнера  
-все тесты проходят  
  
## GitVerse CI  
### Конфигурация  
Файл:  
```text  
.gitverse/workflows/clean_up_pipeline.yaml
```
  
### Логика pipeline  
Pipeline содержит этапы:  
-Checkout repository  
-Build Docker Image  
-Run Tests in Container  
-Quality Gate - Clean Up Resources  
  
### Результат  
Pipeline в GitVerse запускается, но падает на шаге сборки Docker-образа с ошибкой:  
```text  
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```
  
### Вывод по GitVerse  
Облачный раннер GitVerse не предоставляет полноценный доступ к Docker daemon, поэтому сценарий сборки Docker-образа в данном окружении не выполняется.  
Это рассматривается как инфраструктурное ограничение платформы, а не ошибка проекта.  
  
## GitHub Actions  
## Конфигурация  
Файл:  
```text  
.github/workflows/github_pipeline.yml
```
  
### Этапы pipeline  
Pipeline в GitHub Actions содержит следующие шаги:  
-Checkout Code  
-Build Docker Image  
-Run Pytest  
-Quality Gate - Clean Up  
  
Очистка ресурсов выполняется через:  
```YAML  
if: always()
```  
что гарантирует запуск cleanup даже в случае ошибки тестов.  
  
## Демонстрация сценариев  
### 1. Успешный сценарий  
При корректном коде:  
-Docker-образ успешно собирается  
-pytest проходит успешно  
-cleanup выполняется  
-pipeline завершается со статусом Success  
  
### 2. Провальный сценарий  
Для демонстрации ошибки в тесте было намеренно изменено ожидаемое значение в test_scoring.py.  
Результат:  
-шаг Run Pytest завершился ошибкой  
-pipeline стал красным  
-при этом шаг Quality Gate - Clean Up всё равно выполнился благодаря if: always()  
  
### 3. Исправление ошибки  
После возврата корректного ожидаемого значения:  
-тесты снова стали проходить  
-pipeline снова выполнился успешно  
-получен финальный зелёный запуск  
  
## Сравнительный анализ GitVerse и GitHub  
### GitVerse
-pipeline запускается  
-checkout работает  
-Docker build недоступен  
-сценарий ограничен инфраструктурой раннера  
  
### GitHub Actions  
-работает на полноценной Ubuntu VM  
-Docker доступен из коробки  
-Docker build выполняется корректно  
-тесты внутри контейнера выполняются успешно  
-cleanup корректно освобождает место  
  
### Что подтверждено в работе  
Выполнено и продемонстрировано:  
-локальный запуск `pytest`  
-локальная сборка Docker-образа  
-локальный запуск тестов внутри контейнера  
-запуск pipeline в GitVerse  
-ошибка Docker daemon в GitVerse  
-успешный pipeline в GitHub Actions  
-провальный pipeline в GitHub Actions  
-повторный успешный pipeline после исправления  
-выполнение cleanup даже после ошибки тестов  
  
## Скриншоты  
Скриншоты выполнения находятся в папке:  
```text  
docs/
```
  
Использованы следующие файлы:  
`01_project_structure.jpg`  
`02_local_pytest_success.jpg`  
`03_local_docker_build.jpg`  
`04_local_docker_run.jpg`  
`05_gitverse_repo_main.jpg`  
`06_gitverse_ci_runs.jpg`  
`07_gitverse_ci_failed.jpg`  
`08_gitverse_docker_daemon_error.jpg`  
`09_github_repo_main.jpg`  
`10_github_actions_runs.jpg`  
`11_github_failed_run_summary.jpg`  
`12_github_failed_pytest.jpg`  
`13_github_failed_cleanup.jpg`  
`14_github_success_run_summary.jpg`  
`15_github_success_steps.jpg`  
`16_github_success_pytest.jpg`  
`17_github_success_cleanup.jpg`  
  
## Ссылки  
### GitHub  
Основной репозиторий проекта:  
```text  
https://github.com/ghoules3/credit-scoring-ci
```
  
### GitVerse  
Репозиторий для демонстрации запуска pipeline в GitVerse:  
```text  
https://gitverse.ru/ghoules3/credit-scoring-ci
```

## Вывод  
В лабораторной работе реализован CI/CD-конвейер для мини-проекта кредитного скоринга.  
Настроены пайплайны для GitVerse и GitHub, выполнена автоматическая сборка Docker-образа, запуск unit-тестов и очистка ресурсов после завершения pipeline.  
Показано, что:  
-GitVerse имеет ограничения по доступу к Docker daemon в облачном раннере  
-GitHub Actions успешно выполняет весь сценарий  
-при ошибке тестов cleanup всё равно выполняется  
-после исправления кода pipeline снова становится успешным  
