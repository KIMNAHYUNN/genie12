var element = document.querySelector(".door");
element.addEventListener("click", toggleDoor);


function toggleDoor() {
  document.getElementById("knockknock").play(),
            setTimeout(function () {
                tmp = 0,
                    document.body.classList.add("doorOpened")
            }, 0)
  setTimeout(function() {
        element.classList.toggle("doorOpen");
  }, 2000);
  setTimeout('go_url()',3800)  // 5초후 go_url() 함수를 호출한다.
}
function go_url(){
         location.href="../templates/start.html"  // 페이지 이동
      }
//jQuery(function($) {
//    //$("body").css("display", "none");
//    //$("body").fadeIn(1000);
//    $("a.transition").click(function(event){
//        event.preventDefault();
//        linkLocation = this.href;
//        $("body").fadeOut(1000, redirectPage);
//    });
//    function redirectPage() {
//    window.location = linkLocation;
//    }
//});