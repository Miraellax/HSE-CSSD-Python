# Тестирование API

## 1. Получение токена авторизации

### 1.1 Корректный логин и пароль (200 OK)
**Запрос:** 

![img_5.png](img/api_test_imgs/img_5.png)

**Params:** \-

**Authorization:** \-

![img_33.png](img/api_test_imgs/img_33.png)

**Headers:** (Auto-generated)

![img_4.png](img/api_test_imgs/img_4.png)

**Body:**

![img_6.png](img/api_test_imgs/img_6.png)

**Тесты:**

![img_7.png](img/api_test_imgs/img_7.png)

**Результаты тестирования:**

![img_12.png](img/api_test_imgs/img_12.png)

![img_28.png](img/api_test_imgs/img_28.png)

![img_8.png](img/api_test_imgs/img_8.png)

### 1.2 Некорректный логин и пароль (422 Validation Error)
**Запрос:** 

![img_5.png](img/api_test_imgs/img_5.png)

**Params:** \-

**Authorization:** \-

![img_33.png](img/api_test_imgs/img_33.png)

**Headers:** (Auto-generated)

![img_4.png](img/api_test_imgs/img_4.png)

**Body:**

![img_11.png](img/api_test_imgs/img_11.png)

**Тесты:**

![img_9.png](img/api_test_imgs/img_9.png)

**Результаты тестирования:**

![img_13.png](img/api_test_imgs/img_13.png)

![img_29.png](img/api_test_imgs/img_29.png)

![img_10.png](img/api_test_imgs/img_10.png)

## 2. Cоздание задачи

### 2.1 Авторизация, корректные данные (200 OK)
**Запрос:** 

![img_14.png](img/api_test_imgs/img_14.png)

**Params:** 

![img_15.png](img/api_test_imgs/img_15.png)

**Authorization:** 

![img_16.png](img/api_test_imgs/img_16.png)

**Headers:** (Auto-generated)

![img_17.png](img/api_test_imgs/img_17.png)

**Body:** image

![img_18.png](img/api_test_imgs/img_18.png)

**Тесты:**

![img_19.png](img/api_test_imgs/img_19.png)

**Результаты тестирования:**

![img_20.png](img/api_test_imgs/img_20.png)

![img_30.png](img/api_test_imgs/img_30.png)

![img_21.png](img/api_test_imgs/img_21.png)

### 2.2 Авторизация, не корректные данные (400 Bad request)
**Запрос:** 

![img_27.png](img/api_test_imgs/img_27.png)

**Params:** 

![img_26.png](img/api_test_imgs/img_26.png)

**Authorization:** 

![img_16.png](img/api_test_imgs/img_16.png)

**Headers:** (Auto-generated)

![img_17.png](img/api_test_imgs/img_17.png)

**Body:** image

![img_25.png](img/api_test_imgs/img_25.png)

**Тесты:**

![img_24.png](img/api_test_imgs/img_24.png)

**Результаты тестирования:**

![img_22.png](img/api_test_imgs/img_22.png)

![img_31.png](img/api_test_imgs/img_31.png)

![img_23.png](img/api_test_imgs/img_23.png)

### 2.3 Нет авторизации, корректные данные (401 Unauthorized)
**Запрос:** 

![img_32.png](img/api_test_imgs/img_32.png)

**Params:** 

![img_15.png](img/api_test_imgs/img_15.png)

**Authorization:**  \-

![img_33.png](img/api_test_imgs/img_33.png)

**Headers:** (Auto-generated)

![img_34.png](img/api_test_imgs/img_34.png)

**Body:** 

![img_18.png](img/api_test_imgs/img_18.png)

**Тесты:**

![img_35.png](img/api_test_imgs/img_35.png)

**Результаты тестирования:**

![img_36.png](img/api_test_imgs/img_36.png)

![img_37.png](img/api_test_imgs/img_37.png)

![img_38.png](img/api_test_imgs/img_38.png)

### 3. Получение списка задач

### 3.1 Авторизация, корректные данные (200 OK)

**Запрос:** 

![img_39.png](img/api_test_imgs/img_39.png)

**Params:** \-

**Authorization:** 

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated) 

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_43.png](img/api_test_imgs/img_43.png)

**Результаты тестирования:**

![img_44.png](img/api_test_imgs/img_44.png)

![img_45.png](img/api_test_imgs/img_45.png)

![img_46.png](img/api_test_imgs/img_46.png)

### 3.2 Нет авторизации, корректные данные (401 Unauthorized)

**Запрос:** 

![img_40.png](img/api_test_imgs/img_40.png)

**Params:** \-

**Authorization:** \-

![img_47.png](img/api_test_imgs/img_47.png)

**Headers:** (Auto-generated)

![img_48.png](img/api_test_imgs/img_48.png)

**Body:** \-

**Тесты:**

![img_49.png](img/api_test_imgs/img_49.png)

**Результаты тестирования:**

![img_50.png](img/api_test_imgs/img_50.png)

![img_51.png](img/api_test_imgs/img_51.png)

![img_52.png](img/api_test_imgs/img_52.png)

### 4. Получение статуса задачи

### 4.1 Авторизация, корректные данные (200 OK)

**Запрос:** 

![img_53.png](img/api_test_imgs/img_53.png)

**Params:** \-

**Authorization:**

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated) 

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_54.png](img/api_test_imgs/img_54.png)

**Результаты тестирования:**

![img_55.png](img/api_test_imgs/img_55.png)

![img_56.png](img/api_test_imgs/img_56.png)

![img_57.png](img/api_test_imgs/img_57.png)

### 4.2 Авторизация, не корректные данные (404 Bad request)

**Запрос:** 

![img_58.png](img/api_test_imgs/img_58.png)

**Params:** \-

**Authorization:**

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated)

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_59.png](img/api_test_imgs/img_59.png)

**Результаты тестирования:**

![img_60.png](img/api_test_imgs/img_60.png)

![img_61.png](img/api_test_imgs/img_61.png)

![img_62.png](img/api_test_imgs/img_62.png)

### 4.3 Нет авторизации, корректные данные (401 Unauthorized)

**Запрос:** 

![img_63.png](img/api_test_imgs/img_63.png)

**Params:** \-

**Authorization:** \-

![img_47.png](img/api_test_imgs/img_47.png)

**Headers:** (Auto-generated)

![img_48.png](img/api_test_imgs/img_48.png)

**Body:** \-

**Тесты:**

![img_64.png](img/api_test_imgs/img_64.png)

**Результаты тестирования:**

![img_65.png](img/api_test_imgs/img_65.png)

![img_66.png](img/api_test_imgs/img_66.png)

![img_67.png](img/api_test_imgs/img_67.png)

### 5. Получение входных данных задачи

### 5.1 Авторизация, корректные данные (200 OK)

**Запрос:** 

![img_68.png](img/api_test_imgs/img_68.png)

**Params:** \-

**Authorization:** 

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated)

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_69.png](img/api_test_imgs/img_69.png)

**Результаты тестирования:**

![img_70.png](img/api_test_imgs/img_70.png)

![img_71.png](img/api_test_imgs/img_71.png)

![img_72.png](img/api_test_imgs/img_72.png)

### 5.2 Авторизация, не корректные данные (404 Bad request)

**Запрос:** 

![img_73.png](img/api_test_imgs/img_73.png)

**Params:** \-

**Authorization:** 

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated) 

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_74.png](img/api_test_imgs/img_74.png)

**Результаты тестирования:**

![img_75.png](img/api_test_imgs/img_75.png)

![img_76.png](img/api_test_imgs/img_76.png)

![img_77.png](img/api_test_imgs/img_77.png)

### 5.3 Нет авторизации, корректные данные (401 Unauthorized)

**Запрос:** 

![img_78.png](img/api_test_imgs/img_78.png)

**Params:** \-

**Authorization:** \-

![img_47.png](img/api_test_imgs/img_47.png)

**Headers:** (Auto-generated)

![img_48.png](img/api_test_imgs/img_48.png)

**Body:** \-

**Тесты:**

![img_79.png](img/api_test_imgs/img_79.png)

**Результаты тестирования:**

![img_80.png](img/api_test_imgs/img_80.png)

![img_81.png](img/api_test_imgs/img_81.png)

![img_82.png](img/api_test_imgs/img_82.png)

### 6. Получение результата задачи (предсказание)

### 6.1 Авторизация, корректные данные (200 OK)

**Запрос:** 

![img_83.png](img/api_test_imgs/img_83.png)

**Params:** \-

**Authorization:** 

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated) 

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_84.png](img/api_test_imgs/img_84.png)

**Результаты тестирования:**

![img_85.png](img/api_test_imgs/img_85.png)

![img_86.png](img/api_test_imgs/img_86.png)

![img_87.png](img/api_test_imgs/img_87.png)

### 6.2 Авторизация, не корректные данные (404 Bad request)

**Запрос:** 

![img_88.png](img/api_test_imgs/img_88.png)

**Params:** \-

**Authorization:** 

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated) 

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_89.png](img/api_test_imgs/img_89.png)

**Результаты тестирования:**

![img_90.png](img/api_test_imgs/img_90.png)

![img_91.png](img/api_test_imgs/img_91.png)

![img_92.png](img/api_test_imgs/img_92.png)

### 6.3 Нет авторизации, корректные данные (401 Unauthorized)

**Запрос:** 

![img_93.png](img/api_test_imgs/img_93.png)

**Params:** \-

**Authorization:** \-

![img_47.png](img/api_test_imgs/img_47.png)

**Headers:** (Auto-generated)

![img_48.png](img/api_test_imgs/img_48.png)

**Body:** \-

**Тесты:**

![img_94.png](img/api_test_imgs/img_94.png)

**Результаты тестирования:**

![img_95.png](img/api_test_imgs/img_95.png)

![img_96.png](img/api_test_imgs/img_96.png)

![img_97.png](img/api_test_imgs/img_97.png)

### 7. Получение списка моделей

### 7.1 Авторизация, корректные данные (200 OK)

**Запрос:** 

![img_98.png](img/api_test_imgs/img_98.png)

**Params:** \-

**Authorization:** 

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated)

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_99.png](img/api_test_imgs/img_99.png)

**Результаты тестирования:**

![img_100.png](img/api_test_imgs/img_100.png)

![img_101.png](img/api_test_imgs/img_101.png)

![img_102.png](img/api_test_imgs/img_102.png)

### 7.2 Нет авторизации, корректные данные (401 Unauthorized)

**Запрос:** 

![img_103.png](img/api_test_imgs/img_103.png)

**Params:** \-

**Authorization:** \-

![img_47.png](img/api_test_imgs/img_47.png)

**Headers:** (Auto-generated)

![img_48.png](img/api_test_imgs/img_48.png)

**Body:** \-

**Тесты:**

![img_104.png](img/api_test_imgs/img_104.png)

**Результаты тестирования:**

![img_105.png](img/api_test_imgs/img_105.png)

![img_106.png](img/api_test_imgs/img_106.png)

![img_107.png](img/api_test_imgs/img_107.png)

### 8. Удаление задачи 

### 8.1 Авторизация, корректные данные (200 OK)

**Запрос:** 

![img_108.png](img/api_test_imgs/img_108.png)

**Params:** \-

**Authorization:** 

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated) 

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_109.png](img/api_test_imgs/img_109.png)

**Результаты тестирования:**

![img_110.png](img/api_test_imgs/img_110.png)

![img_111.png](img/api_test_imgs/img_111.png)

![img_112.png](img/api_test_imgs/img_112.png)

### 8.2 Авторизация, не корректные данные (404 Bad request)

**Запрос:** 

![img_113.png](img/api_test_imgs/img_113.png)

**Params:** \-

**Authorization:** 

![img_41.png](img/api_test_imgs/img_41.png)

**Headers:** (Auto-generated)

![img_42.png](img/api_test_imgs/img_42.png)

**Body:** \-

**Тесты:**

![img_114.png](img/api_test_imgs/img_114.png)

**Результаты тестирования:**

![img_115.png](img/api_test_imgs/img_115.png)

![img_116.png](img/api_test_imgs/img_116.png)

![img_117.png](img/api_test_imgs/img_117.png)

### 8.3 Нет авторизации, корректные данные (401 Unauthorized)

**Запрос:** 

![img_118.png](img/api_test_imgs/img_118.png)

**Params:** \-

**Authorization:** \-

![img_47.png](img/api_test_imgs/img_47.png)

**Headers:** (Auto-generated)

![img_48.png](img/api_test_imgs/img_48.png)

**Body:** \-

**Тесты:**

![img_119.png](img/api_test_imgs/img_119.png)

**Результаты тестирования:**

![img_120.png](img/api_test_imgs/img_120.png)

![img_121.png](img/api_test_imgs/img_121.png)

![img_122.png](img/api_test_imgs/img_122.png)

### Общие результаты тестирования
![img.png](img/api_test_imgs/img.png)

![img_1.png](img/api_test_imgs/img_1.png)

![img_2.png](img/api_test_imgs/img_2.png)

![img_3.png](img/api_test_imgs/img_3.png)

### Общие результаты работы сервера

![img.png](img/api_test_imgs/img_123.png)

![img_1.png](img/api_test_imgs/img_124.png)

![img_2.png](img/api_test_imgs/img_125.png)