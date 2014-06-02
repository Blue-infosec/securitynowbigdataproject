function dataController($scope, gettwapp){
    gettwapp.episode("020", function(data){
        $scope.$apply(function(){
            $scope.thedata = data;
        });
    });
    console.log("scope", $scope);
    $scope.$watch("searchval", function(){
        console.log("searchval: scope: ", $scope);
        if($scope.searchval.length >= 3){
            gettwapp.search($scope.searchval, function(searchres){
                console.log("Search Results: ", searchres);

                $scope.$apply(function(){
                    $scope.thedata = searchres;
                });

            });
        }

    });


}