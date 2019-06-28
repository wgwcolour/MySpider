function showWords(zlVjhiyMm1) {
            var YB2 = "";
            zlVjhiyMm1['\x73\x70\x6c\x69\x74']("\x7c")['\x66\x6f\x72\x45\x61\x63\x68'](function ($lvd3) {
                if ($lvd3['\x73\x65\x61\x72\x63\x68'](/【(.*?)】/) != -1) {
                    YB2 += $lvd3['\x72\x65\x70\x6c\x61\x63\x65']("\u3010", "")['\x72\x65\x70\x6c\x61\x63\x65']("\u3011", "")
                } else {
                    $lvd3 = $lvd3['\x72\x65\x70\x6c\x61\x63\x65'](/[g-t]/ig, "");
                    YB2 += "\x26\x23\x78" + $lvd3 + "\x3b"
                }
            });
            return YB2
        }


var s = process.argv.splice(2)[0]
console.log(showWords(s))