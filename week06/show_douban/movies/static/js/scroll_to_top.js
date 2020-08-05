(function () {
    var goToTop = function() {
        // $('.js-gotop').on('click', function(event){
        //     event.preventDefault();
        //     $('html, body').animate(
        //         {scrollTop: $('html').offset().top},
        //         500,
        //         'easeInOutExpo'
        //     );
        
        //     return false;
        // });

        $(window).scroll(function(){

            var $win = $(window);
            if ($win.scrollTop() > 200) {
                $('.back-top').addClass('active');
            } 
            else {
                $('.back-top').removeClass('active');
            };

        });
    };
    $(function(){
        goToTop();
    });
}());