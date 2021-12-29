const body = document.body;
let tmp;
window.onload = function () {
    document.getElementById("door").addEventListener("click", function () {
        (body.classList.contains("doorOpened") && tmp !== 1)
        ? (
            document.body.classList.remove("doorOpened")
        )
        : (
            tmp = 1,
            document.getElementById("knockknock").play(),
            setTimeout(function () {
                tmp = 0,
                    document.body.classList.add("doorOpened")
            }, 2000)
        )
    })
}
$(function () {

    $("a").click(function () {
        var url = $(this).attr("href");
        $("body div").animate({
            "opacity": "0",

        },1000, function () {
            document.location.href = url;
        });

        return false;
    });
});
