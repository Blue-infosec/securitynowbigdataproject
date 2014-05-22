var twapp = angular.module("tw_app", ['ngRoute', 'twAppServices']);


twapp.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider.when("/", {template: '<securitynow twapp="100"></securitynow>', controller: ""});
}]);

function twappController($scope, gettwapp){
    console.log("GETTWAPP twappController: ", twapp);
}

function mainController($scope, gettwapp){

}

function searchController($scope, gettwapp){

}

function dataController($scope, gettwapp){
    gettwapp.episode("020", function(data){
        $scope.$apply(function(){
            $scope.thedata = data;
        });
    });
}

twapp.directive("secnow", function(gettwapp){

    console.log("Project INITIALIZED!!!!");

    var template = '<div class="{{ rmatdat.sentiment }}">' +
        '<div class="episode">{{ rmatdat.episode }}</div>' +
        '' +
        '<div class="name">{{ rmatdat.speaker }}</div>' +
        '<div class="description">{{ rmatdat.original }}</div>' +
        '<div class="highlight">{{ rmatdat.sentiment }}</a>' +
        '</div>';

    return {
        restrict:'E',
        scope: {
            rmatdat:"=chez"
        },
        template: template,
        link: function (scope, element, attr){
//            gettwapp.episode("020", function(data){
//                console.log("DATA FROM SERVER: ");
//                console.log(data);
//                $scope.data = data;
//            });
        }
    }

});