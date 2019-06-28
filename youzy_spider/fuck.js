eval(function (p, a, c, k, e, d) {
            e = function (c) {
                return (c < a ? "" : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
            };
            if (!''.replace(/^/, String)) {
                while (c--) d[e(c)] = k[c] || e(c);
                k = [function (e) {
                    return d[e]
                }];
                e = function () {
                    return '\\w+'
                };
                c = 1;
            };
            while (c--)
                if (k[c]) p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c]);
            return p;
        }('4 5=3(2){4 1="";2.7("|").6(3(0){0=0.b(/[c-d]/8,"");1+="&#9"+0+";"});a 1}', 14, 14, 'value|number|myNumbers|function|var|showNumber|forEach|split|ig|x|return|replace|g|t'.split('|'), 0, {}))

var s = process.argv.splice(2)[0]
var resultList = s.split(",")
var result = new Array();
for(i = 0;i<resultList.length;i++){
    if(resultList[i] != 0)
        result[i] = showNumber(resultList[i].substring(0, resultList[i].length - 1))
    else result[i]=0
};
res = result.join(",")


//console.log(result)
console.log(res)
//console.log(fractionsProfessionsQuery(input))