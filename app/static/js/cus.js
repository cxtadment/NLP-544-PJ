/**
 * Created by zjjcxt on 4/17/16.
 */
$( document ).ready(function() {
    $('.search-keywords').click(function(e){
        text = $.trim($('.search-input').val());
        if (!text || text == null ) {
            $('.validation').show()
        } else {
            $('.validation').hide()
        }
        getSearchResultAjax(text)
    });

    function getSearchResultAjax(text) {
        $.ajax({
          url: "/searchApi",
          type: "GET",
          data: {keyword : text},
          dataType: "json",
          success: function(data){
            //$("#results").append(html);
          }
        });
    }
});