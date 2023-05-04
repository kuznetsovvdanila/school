$(document).ready(function() {
    var topMenu = $('.top_menu'); // выбираем объект класса top_menu
    var menuHeight = topMenu.height(); // получаем высоту объекта top_menu
    var isChangingOpacity = false;

    // функция для изменения прозрачности фона
    function changeOpacity(isChanging, duration=300) {
        var a;
        if (isChanging) {
            start = 0;
            end = 1;
        } else {
            start = 1;
            end = 0;
        }
        var startTime = null;
      
        function update(currentTime) {
          if (!startTime) {
            startTime = currentTime;
          }
          var progress = currentTime - startTime;
          var opacity = start + (end - start) * (progress / duration);
          topMenu.css('background-color', `rgba(0, 0, 0, ${opacity})`);
          if (progress < duration) {
            requestAnimationFrame(update);
          } else {
            isChangingOpacity = !isChanging;
          }
        }
        if (isChangingOpacity == isChanging) {
            requestAnimationFrame(update);
        };
      }

    // устанавливаем начальный background-color
    topMenu.css('background-color', 'rgba(0, 0, 0, 1)');
  
    // функция для изменения background-color в зависимости от положения скролла
    $(window).scroll(function() {
      if ($(this).scrollTop() >= menuHeight) {
        changeOpacity(false);
      } else {
        changeOpacity(true);
      }
    });
  
    // функция для изменения background-color при наведении на объект
    topMenu.hover(function() {
        changeOpacity(true);
    }, function() {
      if ($(window).scrollTop() >= menuHeight) {
        changeOpacity(false);
      } else {
        changeOpacity(true);
      }
    });
});
  