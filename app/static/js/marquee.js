$(document).ready(function () {
    const images = $('.clients-logo img');
    const containerWidth = $('.clients-logo').width();

    // Set initial position of each image
    let totalWidth = 0;
    const gap = 10;
    images.each(function () {
        $(this).css('left', totalWidth);
        totalWidth += $(this).width() + gap;
    });

    function animateMarquee() {
        images.each(function () {
            const img = $(this);
            img.animate({ 'left': '-=1' }, 0, function () {
                if (img.position().left + img.width() <= 0) {
                    img.appendTo('.clients-logo').css('left', totalWidth - img.width());
                }
            });
        });
    }

    setInterval(animateMarquee, 10);
});