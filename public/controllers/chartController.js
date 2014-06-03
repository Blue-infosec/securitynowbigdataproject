function chartController($scope, gettwapp){

//    gettwapp.happy($scope.searchval, function(data){
//        $scope.$apply(function(){
//            $scope.thedata = data.data;
//            $scope.count = data.count;
//        });
//    });

    console.log("IN CHART CONTROLLER")
    $scope.options = {
        series: [
            {
                y: "val_0",
                label: "Leo Pos",
                color: "#1f77b4",
                type: "line",
                thickness: "3px"
            },
            {y: "val_1", label: "Steve Pos", color: "#ff7f0e", type: "line", thickness: "3px"},
            {
                y: "val_3",
                label: "Pos difference",
                color: "#2ca02c",
                type: "area",
                thickness: "1px"
            }
        ],
        axes: {x: {type: "linear", key: "x"}, y: {type: "linear"}},
        lineMode: "linear",

        tooltipMode: "default"
    };
    $scope.data = [
        {x: 0, val_0: 12, val_1: 67, val_2: 12, val_3: 12},
        {x: 1, val_0: 23, val_1: 74, val_2: 53, val_3: 86},
        {x: 2, val_0: 42, val_1: 17, val_2: 18, val_3: 12},
        {x: 3, val_0: 67, val_1: 52, val_2: 37, val_3: 95},
        {x: 4, val_0: 22, val_1: 88, val_2: 22, val_3: 34},
        {x: 5, val_0: 34, val_1: 12, val_2: 15, val_3: 22},
        {x: 6, val_0: 15, val_1: 45, val_2: 34, val_3: 45},
        {x: 7, val_0: 55, val_1: 34, val_2: 51, val_3: 34},
        {x: 8, val_0: 64, val_1: 15, val_2: 77, val_3: 25},
        {x: 9, val_0: 24, val_1: 48, val_2: 15, val_3: 33},
        {x: 10, val_0: 33, val_1: 31, val_2: 22, val_3: 29},
    ];


}