angular.module("tw_app").directive('securitynow', function (gettwapp) {
    var template = '<dl class="gettwapp" ng-repeat="">' +
        '<dt><a class="gettwappInstance" href="{{gettwapp.id}}">{{gettwapp.title}}</a></dt>' +
        '</dl>';
              console.log("DIRECTIVE IS FINALLY BEING CALLED!!!");
    return {
        restrict:'E',
        scope:{ twapp:"="},
        template:template,
        link:function (scope, lelement, attrs) {
            gettwapp.episode(scope.twapp, function (data) {
                console.log("HOLY CRAP LOOK AT THIS DATA!: ", data);
                lelement.find("dl").append("<dd class=\"actualdata\">" + data + "</dd>");
            });
        }
    }
});