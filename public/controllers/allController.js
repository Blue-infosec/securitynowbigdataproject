function allController($scope, gettwapp){
    gettwapp.fullset(function(data){
        $scope.$apply(function(){
            $scope.thedata = data;
        });
    });


}