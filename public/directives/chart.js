twapp.directive("chartDisplay", function(gettwapp){

    console.log("Charts INITIALIZED!!!!");

    var template = '<div class="{{ rmatdat.sentiment }}">' +
        '<div class="episode">{{ rmatdat.episode }}</div>' +
        '' +
        '<div class="name">{{ rmatdat.speaker }}</div>' +
        '<div class="description">{{ rmatdat.original }}</div>' +
        '<div class="highlight badge alert-success">{{ rmatdat.sentiment }}</a>' +
        '</div>';

    return {
        restrict:'E',
        scope: {
            rmatdat:"=chez"
        },
        template: template,
        link: function (scope, element, attr){

        }
    }

});