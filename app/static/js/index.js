// console.log("hello");

// Show and hide password
var show = document.querySelector("#show_hide_password");
var icon_show = show.querySelector(".icon-check");
icon_show.getAttribute("whenClicked");

icon_show.addEventListener("click", () => {
  var arri = icon_show.querySelectorAll("i");
  arri.forEach((e) => {
    var Master_check = {
      classListe: e.classList.value,
      addClass: e.classList,
      show_pss: show.querySelector("input"),
      type: ["fa fa-eye-slash", "fa fa-eye fa-eye-slash"],
      addtype: ["fa-eye-slash", "fa-eye"],
      addshow: ["text", "password"],
    };

    var check;
    Master_check.type.map((e) => {
      check = e === Master_check.classListe ? true : false;
      boolCheck(check);
    });

    function boolCheck(check) {
      if (check === true) {
        Master_check.addClass.remove(Master_check.addtype[0]);
        Master_check.addClass.add(Master_check.addtype[1]);
        Master_check.show_pss.type = Master_check.addshow[0];
      } else {
        Master_check.show_pss.type = Master_check.addshow[1];
        Master_check.addClass.add(Master_check.addtype[0]);
      }
    }
  });
});
