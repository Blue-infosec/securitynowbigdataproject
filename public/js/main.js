var twapp = angular.module("tw_app", ['ngRoute', 'twAppServices']);


twapp.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider.when("/", {template: '/templates/twapp.tpl', controller: ""});
        $routeProvider.when("/all", {template: '/templates/all.tpl', controller: "allController"});
        $routeProvider.when("/single", {template: '/templates/single.tpl', controller: "singleController"});
}]);
