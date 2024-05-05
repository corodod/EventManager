var notificationsSent = [];

function showNotification(event) {
    if (!notificationsSent.includes(event.date + event.time)) {
        var notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = 'Событие: ' + event.event + '\nДата: ' + event.date + '\nВремя: ' + event.time;
        document.body.appendChild(notification);
        setTimeout(function() {
            notification.style.display = 'none';
        }, 5000);
        notificationsSent.push(event.date + event.time);
    }
}

function checkEvents() {
    fetch('/get_event_data')
        .then(response => response.json())
        .then(data => {
            var currentDate = new Date();
            data.events.forEach(function (event) {
                var eventDate = new Date(event.date + ' ' + event.time);
                if (eventDate <= currentDate && !notificationsSent.includes(event.date + event.time)) {
                    showNotification(event);
                }
            });
        });
}

setInterval(checkEvents, 60000);
window.onload = function() {
    checkEvents();
};
