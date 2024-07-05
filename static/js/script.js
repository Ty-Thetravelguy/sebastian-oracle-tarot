$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: 'dd mmm, yyyy', 
        yearRange: 60 
    });
    $('.timepicker').timepicker();
});

// script.js

$(document).ready(function() {
    // Initialize materialize components
    M.AutoInit();

    // Form submission logic
    $('#tarot-form').on('submit', function(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        $.ajax({
            url: '/tarot_reading',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                localStorage.setItem('tarotReadingData', JSON.stringify(data));
                window.location.href = '/reading';
            }
        });
    });

    // Load tarot reading data
    if (window.location.pathname === '/reading') {
        setTimeout(function() {
            $('#shuffling-image').hide();
            const data = JSON.parse(localStorage.getItem('tarotReadingData'));
            if (data) {
                const cardContainer = $('#cards-container');
                data.selected_cards.forEach(card => {
                    const cardElement = $(`
                        <div class="col s4 m2">
                            <img src="${card.cardImg}" alt="${card.cardName}" class="responsive-img">
                            <p class="center-align grey-text text-lighten-5">${card.cardName}</p>
                        </div>
                    `);
                    cardContainer.append(cardElement);
                });
                $('#reading-output').text(data.reading_output);
                $('#reading-result').show();
            }
        }, 10000); // 10 seconds
    }
});
