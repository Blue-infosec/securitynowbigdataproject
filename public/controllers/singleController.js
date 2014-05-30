function singleController($scope, gettwapp){
    $scope.searchval = "042";

    gettwapp.episode($scope.searchval, function(data){
        $scope.$apply(function(){
            $scope.thedata = data;
        });
    });

    $scope.$watch("singlesearchvalue", function(){
        console.log("singlesearchvalue: scope: ", $scope);
        if($scope.singlesearchvalue.length > 2){
            gettwapp.episode($scope.singlesearchvalue, function(searchres){
                console.log("Search Results: ", searchres);

                $scope.$apply(function(){
                    $scope.thedata = searchres;
                });

            });
        }

    });


}