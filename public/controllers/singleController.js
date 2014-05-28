function singleController($scope, gettwapp){
    $scope.searchval = "004";

    gettwapp.episode($scope.searchval, function(data){
        $scope.$apply(function(){
            $scope.thedata = data;
        });
    });

    $scope.watch("searchval", function(){
        console.log("searchval: scope: ", $scope);
        if($scope.searchval.length > 3){
            gettwapp.search($scope.searchval, function(searchres){
                console.log("Search Results: ", searchres);

                $scope.$apply(function(){
                    $scope.thedata = searchres;
                });

            });
        }

    });


}