$(document).ready(function() {
    $(".add-to-cart").each(function() {
        $(this).click(function() {
            let url = $(this).data('href');
            if ($(this).data('logged-user') === "True") {
                $.ajax({
                    type: "GET",
                    url: url,
                    success: function(data) {
                        $("sup.badge").text(data.quantity);
                        $("#alert-add-product").show();
                        setTimeout(function() {
                            $("#alert-add-product").hide();
                        }, 1000);
                    },
                    error: function(xhr, textStatus, errorThrow) {
                        console.log(errorThrow);
                    }
                })
            }
            else {
                window.location.href = url;
            }
        });
    });
});

