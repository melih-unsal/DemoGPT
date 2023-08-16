document.addEventListener("DOMContentLoaded", function() {
document.getElementById("appButton").addEventListener("click", function() {
    var iframe = document.createElement("iframe");
    iframe.src = "https://demogpt.streamlit.app/?embed=true";
    iframe.style.width = "80%";
    iframe.style.height = "80vh";
    iframe.style.position = "fixed";
    iframe.style.top = "10%";
    iframe.style.left = "10%";
    iframe.style.zIndex = "1000";
    iframe.style.border = "none";
    document.body.appendChild(iframe);

    // Add an overlay background to emphasize the iframe
    var overlay = document.createElement("div");
    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    overlay.style.zIndex = "999";
    document.body.appendChild(overlay);

    // Close the iframe when clicking outside
    overlay.addEventListener("click", function() {
        document.body.removeChild(iframe);
        document.body.removeChild(overlay);
    });
});
});
