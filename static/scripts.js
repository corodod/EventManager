var notificationsSent = [];

function showNotification(event) {
    var notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = 'Событие: ' + event.event + '\nДата: ' + event.date + '\nВремя: ' + event.time;
    document.body.appendChild(notification);
    setTimeout(function() {
        notification.style.display = 'none';
    }, 5000);
}

function checkEvents() {
    fetch('/get_event_data')
        .then(response => response.json())
        .then(data => {
            var currentDate = new Date();
            data.events.forEach(function (event) {
                var eventDate = new Date(event.date + 'T' + event.time + ':00');
                if (eventDate <= currentDate && !notificationsSent.includes(event.date + event.time)) {
                    showNotification(event);
                    notificationsSent.push(event.date + event.time);
                }
            });
        });
}

// Вызываем функцию checkEvents() каждые 60 секунд
setInterval(checkEvents, 60000);
