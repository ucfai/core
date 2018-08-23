document.addEventListener("DOMContentLoaded", function() {
    var nav = $("#meeting-toc")
    $$("h2").forEach(function (h2) {
        if (h2.parentNode.id) {
            $.create("a", {
                href: "#" + h2.parentNode.id,
                textContent: h2.textContent.replace(/\(.+?\)/g, ""),
                inside: nav
            });
        }
    });
});