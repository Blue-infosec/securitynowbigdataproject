function chartController($scope, gettwapp){
    gettwapp.fullSet(100, 1, function(data){
        $scope.$apply(function(){
            $scope.thedata = data.data;
            $scope.count = data.count;
        });
    });

    $scope.Chart01options = {
        axes: {
            x: {key: 'x', labelFunction: function(value) {return value;}, type: 'linear', tooltipFormatter: function(x) {return x;}},
            y: {type: 'linear'},
            y2: {type: 'linear'}
        },
        series: [
            {y: 'value', color: 'steelblue', thickness: '2px', type: 'area', striped: true, label: 'Pouet'},
            {y: 'otherValue', axis: 'y2', color: 'lightsteelblue'}
        ],
        lineMode: 'linear',
        tension: 0.7
    }


}