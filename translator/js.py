bd_js_code = r'''
function a(r) {
        if (Array.isArray(r)) {
            for (var o = 0, t = Array(r.length); o < r.length; o++)
                t[o] = r[o];
            return t
        }
        return Array.from(r)
    }
    function n(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
            var a = o.charAt(t + 2);
            a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
    }
    function e(r) {
        var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === o) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
        } else {
            for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                C !== h - 1 && f.push(o[C]);
            var g = f.length;
            g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
        }
        var u = void 0
          , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        u = null !== i ? i : (i = window[l] || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
            S[c++] = A >> 18 | 240,
            S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
            S[c++] = A >> 6 & 63 | 128),
            S[c++] = 63 & A | 128)
        }
        for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
            p += S[b],
            p = n(p, F);
        return p = n(p, D),
        p ^= s,
        0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
        p.toString() + "." + (p ^ m)
    }
    function s(a,t,s,j,N){var O=null,C=null,I="",E={0:"translator",1:"keyWord",2:"simpleMeaning",3:"oxford",4:"collins",5:"en2en",6:"zh2en",7:"zh2zh",8:"illSen",9:"wordColl",10:"webMeaning",11:"synonym",12:"rootsaffixes",13:"usecase",14:"sanyms",15:"etym"},W={translator:!1,keyWord:!1,simpleMeaning:!1,festivalLink:window.festivalLinkInfo.isShowFestivalLink,adLink:window.adLinkInfo.isShowAdLink,oxford:!1,collins:!1,en2en:!1,zh2en:!1,zh2zh:!1,illSen:!1,wordColl:!1,webMeaning:!1,synonym:!1,rootsaffixes:!1,usecase:!1,sanyms:!1,etym:!1};
!function(){if(!a.dict_result||"en"!==s&&"zh"!==s&&"jp"!==s&&"th"!==s)O=!1,k.sendIndexBannerLog();else if(a.dict_result.content)N||(O=a.dict_result,C=a.dict_result.baike_img_url,I=JSON.stringify(a.dict_result));
else if(a.dict_result.simple_means&&!N&&(O=a.dict_result.simple_means,C=a.dict_result.baike_img_url,a.dict_result.simple_means.symbols&&a.dict_result.simple_means.symbols.length>0&&(I=JSON.stringify({simple_means:{symbols:a.dict_result.simple_means.symbols}})),a.dict_result.sim_words&&(O.sim_words=a.dict_result.sim_words),a.dict_result.net_means&&(O.net_means=a.dict_result.net_means)),"zh"===t&&"en"===s||"en"===t&&"zh"===s)for(var e in a.dict_result)if(a.dict_result[e]instanceof Object&&!$.isEmptyObject(a.dict_result[e])&&0!==a.dict_result[e].length)switch(e){case"collins":W.collins=!0;
break;case"synthesize_means":W.zh2en=!0;break;case"zdict":W.zh2zh=!0;break;case"edict":W.en2en=!0;break;case"oxford":W.oxford=!0;
break;case"general_knowledge":a.dict_result.general_knowledge.similar_words&&(W.wordColl=!0);break;case"netdata":W.webMeaning=!0;
break;case"synonym":W.synonym=!0;break;case"rootsaffixes":W.rootsaffixes=!0;break;case"usecase":W.usecase=!0;break;case"sanyms":W.sanyms=!0;
break;case"etym":W.etym=!0}W.simpleMeaning=Boolean(O),!a.liju_result||"en"!==s&&"zh"!==s||!a.liju_result["double"]&&!a.liju_result.single||(W.illSen=!0),a.trans_result&&a.trans_result.keywords&&a.trans_result.keywords.length>0&&("zh"===t&&"en"===s||"en"===t&&"zh"===s)&&!W.simpleMeaning&&(W.keyWord=!0),a.simworks&&"[object Object]"===Object.prototype.toString.call(a.simworks)&&(W.translator=!0)
}();var B=[],F=!1;!function(){if(e("translation:widget/translate/sideNav/navSorter/listOperator").getNavList().forEach(function(e){var a=E[e];
W[a]&&B.push(a)}),W.festivalLink||W.adLink){var a=[];W.festivalLink&&a.push("festivalLink"),W.adLink&&a.push("adLink"),"simpleMeaning"!==B[0]?(B.unshift.apply(B,a),W.adLink&&W.festivalLink&&(F=!0)):B.splice.apply(B,[1,0].concat(a))
}var t=B.find(function(e){return"festivalLink"!==e&&"adLink"!==e});n.set("firstModuleId",parseInt(Object.keys(E).find(function(e){return E[e]===t
}),10))}();var D=a.dict_result;B.forEach(function(e){switch(e){case"translator":l.build(a.simworks);break;case"keyWord":m.build({data:a.trans_result.keywords,from:t,to:s});
break;case"simpleMeaning":d.buildSimpleMeans({data:O,to:s,baikeImgUrl:C});break;case"festivalLink":r.buildFestivalLink();
break;case"adLink":o.build(F);break;case"oxford":v.init(D.oxford);break;case"collins":g.buildCollins({data:D.collins});break;
case"en2en":c.buildEdict({data:D.edict});break;case"zh2en":_.buildDict({data:D.synthesize_means});break;case"zh2zh":u.buildZdict({data:D.zdict});
break;case"illSen":w.buildSample({data:a.liju_result,from:t,to:s,query:j,badCaseByForce:N});break;case"wordColl":p.buildGeneral({data:D.general_knowledge});
break;case"webMeaning":h.buildWebMeans({data:D});break;case"synonym":z.buildSynonym({data:D.synonym});break;case"rootsaffixes":L.buildRootsaffixes({data:D.rootsaffixes});
break;case"usecase":x.buildUsecase({data:D.usecase});break;case"sanyms":M.buildSanyms({data:D.sanyms});break;case"etym":S.buildEtym({data:D.etym})
}});var J=!1;for(var q in W)J=J||W[q];J&&i.showAppQr(F),b.init({from:t,to:s,query:j,dictJSON:I}),"en"===t&&"zh"===s||"zh"===t&&"en"===s?(y.genCollapse(),f.genNav()):f.destroyNav()
}
'''


gg_js_code = '''
    function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;
        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";
        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };
    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
'''
