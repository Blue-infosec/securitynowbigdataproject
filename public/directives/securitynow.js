twapp.directive("secnow", function(gettwapp){

    console.log("Project INITIALIZED!!!!");

    var template = '' +
        '<div class="sencontain">' +
        '<div class="{{ rmatdat.sentiment }}"></div>' +
        '<div class="wrdcontain">' +
        '<div class="episode">{{ rmatdat.episode }}</div>' +
        '<div class="name">{{ rmatdat.speaker }}</div>' +
        '<div class="description">{{ rmatdat.original }}</div>' +
        '</div>' +
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

twapp.directive("secnowall", function(gettwapp){

    console.log("Project INITIALIZED!!!!");

    var template = '' +
        '<div>' +
        '<div class="{{ if rmatdat.sentiment }}" width="50px" height="50px">Chez</div>' +
        '<div class="episode">{{ rmatdat.episode }}</div>' +
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