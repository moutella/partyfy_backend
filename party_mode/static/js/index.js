jQuery(document).ready(function () {
    jQuery("#enter_session").on("submit", function (e) {
        e.preventDefault();
        let session_id=jQuery("#session_id").val();
        console.log(session_id);
        window.location.href = "/session/"+session_id+"/";
    });
});