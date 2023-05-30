const socket = new WebSocket('ws://samotokhin_school.com/lk');

// При открытии соединения
socket.onopen = function() {
  console.log('WebSocket connection established.');
};

// При закрытии соединения
socket.onclose = function(event) {
  console.log('WebSocket connection closed with code:', event.code);
};

// При получении сообщения от сервера
socket.onmessage = function(event) {
  const message = JSON.parse(event.data);
  console.log('Received message:', message);
};

// При возникновении ошибки
socket.onerror = function(error) {
  console.error('WebSocket error:', error);
};
