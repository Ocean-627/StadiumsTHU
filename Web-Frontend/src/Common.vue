<script>
// used for global variables
var colorType = 0

export default {
    colorType,
    fix_reserves: function(reserves, open_times) {
        let k = 0
        let res = []
        let close_times = []
        let i = 0, j = 0
        let e = "00:00"
        for(; i < open_times.length; i++){
            if(e != open_times[i].start){
                close_times.push({
                    type: -1,
                    start: e,
                    end: open_times[i].start
                })
            }
            e = open_times[i].end
        }
        close_times.push({
            type: -1,
            start: e,
            end: "24:00"
        })

        i = j = 0
        let tmp = []
        while(i < close_times.length && j < reserves.length){
            if(close_times[i].start < reserves[j].startTime){
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
            if(e != tmp[i].start){
                res.push({
                    type: 0,
                    start: e,
                    end: tmp[i].start
                })
            }
            res.push(tmp[i])
            e = tmp[i].end
        }

        return res
    }
}
</script>