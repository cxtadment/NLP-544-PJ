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
            $('#loading').show();
            getSearchResultAjax(text)
        }
    });

    function getSearchResultAjax(text) {
        $.ajax({
          url: "/searchApi",
          type: "GET",
          data: {keyword : text},
          dataType: "json",
          success: function(data){
            $('#loading').hide();
            microblogs = data.result;
            all_html = ''
            $.each(microblogs, function(k, v){
                console.log(v)
                text = v.text
                filter_text = v.filter_text
                confidence = v.confidence
                polarity = v.polarity
                keywords = v.words
                content_html = constructHtml(text, filter_text, confidence, keywords, polarity)
                all_html += content_html
            });
            $('.content-microblogs').html(all_html)
          }
        });
    }

    //<div class="list-group result-display">
    //  <a href="#" class="list-group-item list-display">
    //    <div>Microblog Content:</div>
    //    <div>Polarity: </div>
    //    <div>Confidence: </div>
    //    <div>Keywords: </div>
    //  </a>
    //</div>
    function constructHtml(text, filter_text, confidence, keywords, polarity) {
        keywordsHtml = '<span class="keywords">'
        $.each(keywords, function(k, v){
            keywordsHtml += v + ', '
        });
        polarityHtml = ''
        if (polarity == 'pos') {
            polarityHtml += '<a href="#" class="btn btn-info btn-sm"><span class="glyphicon glyphicon-thumbs-up"></span> Positive</a>'
        } else if (polarity == 'neg') {
            polarityHtml += '<a href="#" class="btn btn-info btn-sm"><span class="glyphicon glyphicon-thumbs-down"></span> Negative</a>'
        }
        keywordsHtml += '</span>'
        contentHtml = '<div class="list-group result-display"><a href="#" class="list-group-item list-display">'
        contentHtml += '<div class="item">Microblog Origin Text: <span class="item-text1">'+text+'</span></div>'
        contentHtml += '<div class="item">Microblog Text After filter: <span class="item-text2">'+filter_text+'</span></div>'
        contentHtml += '<div class="item">Polarity: '+polarityHtml+'</div>'
        contentHtml += '<div class="item">Confidence <span class="item-text3">:'+confidence+'%</span></div>'
        contentHtml += '<div class="item">Keywords:'+keywordsHtml+'</div>'
        contentHtml += '</a></div>'

        return contentHtml

    }

});