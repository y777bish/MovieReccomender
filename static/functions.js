$(document).ready(function() {
    var enumData = $("#movies-list").data("enum-data");
    $("#movies-list").select2({
        data:enumData
    })
});

$(document).ready(function() {
    $("#similar-generation").click(function(e) {
    window.location.href = "/about";
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var section = document.querySelector('.section');
    setTimeout(function() {
        section.classList.add('fadeIn');
      }, 1000);
  });