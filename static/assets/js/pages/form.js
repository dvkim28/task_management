document.addEventListener("DOMContentLoaded", function() {
        var form = document.getElementById('generalform');

        // Добавляем слушатель события изменения в форме
        form.addEventListener('change', function() {
            // Создаем объект FormData для сбора данных формы
            var formData = new FormData(form);

            // Создаем объект XMLHttpRequest для отправки данных на сервер
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '', true); // Пустая строка означает отправку на текущий URL

            // Отправляем данные формы на сервер
            xhr.send(formData);
        });
    });