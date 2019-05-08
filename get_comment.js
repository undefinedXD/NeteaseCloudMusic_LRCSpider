const puppeteer = require('puppeteer');
const fs = require('fs');

async function get_comment(song_id,song_name)  {
    const browser = await (puppeteer.launch({ headless: true,timeout: 30000,}));
    const page = await browser.newPage();
    const preurl = 'https://music.163.com/#/song?id=';
    s_id = String(song_id);
    var url = preurl + s_id;
    await page.goto(url);
    await page.waitFor(2000);
    let iframe = await page.frames().find(f => f.name() === 'contentFrame');

    const commentList = await iframe.$$eval('.itm', elements => {
        const cmt = elements.map(v => {
            return v.innerText.replace(/\s/g,'');
        });
        return cmt;
    });

    let writeStream2 = fs.writeFileSync('评论.txt',song_name+'\n'+JSON.stringify(commentList,null,'\t')+'\n',{flag:'a+'});
    browser.close();
    process.exit(0);
};

