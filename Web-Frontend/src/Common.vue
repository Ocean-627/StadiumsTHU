<script>
// used for global variables
var colorType = 0

export default {
    colorType,
    fix_reserves: function(reserves) {
        let k = 0
        let res = []
        let close_times = []
        let i = 0, j = 0
        let e = "00:00"

        for(; i < reserves.length; i++){
            if(e != reserves[i].startTime){
                close_times.push({
                    type: -1,
                    startTime: e,
                    endTime: reserves[i].startTime
                })
            }
            e = reserves[i].endTime
        }
        close_times.push({
            type: -1,
            startTime: e,
            endTime: "24:00"
        })

        i = j = 0
        let tmp = []
        while(i < close_times.length && j < reserves.length){
            if(close_times[i].startTime < reserves[j].startTime){
                tmp.push(close_times[i++])
            }
            else{
                tmp.push(reserves[j++])
            }
        }
        while(i < close_times.length){
            tmp.push(close_times[i++])
        }
        while(j < reserves.length){
            tmp.push(reserves[j++])
        }

        e = "00:00"
        i = 0
        for(; i < tmp.length; i++){
            if(e != tmp[i].startTime){
                res.push({
                    type: 0,
                    startTime: e,
                    endTime: tmp[i].startTime
                })
            }
            res.push(tmp[i])
            e = tmp[i].endTime
        }

        return res
    }
}
</script>