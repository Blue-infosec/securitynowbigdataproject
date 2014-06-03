twapp.directive("counter", function (gettwapp) {

    console.log("counter INITIALIZED!!!!");

    var template = '<div>Steve Has {{ hsteve }} Positive Comments</div>' +
        '<div>Leo Has {{ hleo }} Positive Comments</div>'+
        '<div>Steve Has {{ msteve }} Negative Comments</div>' +
        '<div>Leo Has {{ mleo }} Negative Comments</div>';

    return {
        restrict: 'E',
        scope: {
            number: "=val"
        },
        template: template,
        controller: function ($scope, $element) {
            $scope.singlesearchvalue = "042";

            gettwapp.happy("042", function (data) {
                console.log("DATA FOR SENTIMENT: ", data);
                $scope.$apply(function(){
                    $scope.hleo = data.leo;
                    $scope.hsteve = data.steve;
                });

            });
            gettwapp.mad("042", function (data) {
                console.log("DATA FOR SENTIMENT: ", data);
                $scope.$apply(function(){
                    $scope.mleo = data.leo;
                    $scope.msteve = data.steve;
                });

            });

            elmscope = angular.element(document.getElementById('singlesearch')).scope();

            elmscope.$watch("singlesearchvalue", function () {
                if (elmscope.singlesearchvalue.length > 2) {
                    gettwapp.happy(elmscope.singlesearchvalue, function (data) {
                        console.log("DATA FOR SENTIMENT: ", data);
                        $scope.$apply(function(){
                            $scope.hleo = data.leo;
                            $scope.hsteve = data.steve;
                        });

                    });
                    gettwapp.mad(elmscope.singlesearchvalue, function (data) {
                        console.log("DATA FOR SENTIMENT: ", data);
                        $scope.$apply(function(){
                            $scope.mleo = data.leo;
                            $scope.msteve = data.steve;
                        });

                    });
                }
            });
        }
    }

});