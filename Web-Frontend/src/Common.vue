<script>
// used for global variables
var colorType = 0

export default {
    colorType,
    fix_reserves: function(reserves) {
        let k = 0
        let res = []
        let durations = []
        let i = 1, j = 0
        let e = reserves[0].endTime
        var type;
        if ((reserves[0].openState === true)&&(reserves[0].accessible === true)){
            type = 0;
        }
        else if (reserves[0].openState === false){
            type = 2;
        }
        else{
            type = 1;
        }
        durations.push({type: type, startTime: reserves[0].startTime, endTime: reserves[0].endTime})
        for(i = 1; i < reserves.length; i++){
            var type;
            if ((reserves[i].openState === true)&&(reserves[i].accessible === true)){
                type = 0;
            }
            else if (reserves[i].openState === false){
                type = 2;
            }
            else{
                type = 1;
            }
            durations.push({
                type: type,
                startTime: reserves[i].startTime,
                endTime: reserves[i].endTime
            })
            if(e != reserves[i].startTime){
                durations.push({
                    type: -1,
                    startTime: e,
                    endTime: reserves[i].startTime
                })
            }
            e = reserves[i].endTime
        }
        var compare = function(obj1,obj2){
            var value1 = obj1["startTime"];
            var value2 = obj2["startTime"];
            if (value2 > value2){
                return 1;
            }
            else if (value1<value2){
                return -1;
            }
            else{
                return 0;
            }
        }
        return durations.sort(compare)
    }
}
</script>