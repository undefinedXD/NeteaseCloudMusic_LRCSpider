const puppeteer = require('puppeteer');
const fs = require('fs'); //NodeJS中读写文件的模块

(async () => {
    const browser = await (puppeteer.launch({ headless: false }));
    const page = await browser.newPage();
    await page.goto("https://music.163.com/#");

    const musicName = '借我'
    await page.type('#srch', musicName, { delay: 0 });
    await page.keyboard.press('Enter');

    await page.waitFor(2000);
    let iframe = await page.frames().find(f => f.name() == 'contentFrame');
    const SONG_LS_SELECTOR = await iframe.$('.srchsongst');

    const selectedSongHref = await iframe.evaluate(e => {
        const songList = Array.from(e.childNodes);
        const idx = songList.findIndex(v => v.childNodes[1].innerText.replace(/\s/g, '') === '借我');
        return songList[idx].childNodes[1].firstChild.firstChild.firstChild.href;
    }, SONG_LS_SELECTOR);//定义同时传递 --- 匿名函数？

    await page.goto(selectedSongHref);

    await page.waitFor(2000);
    iframe = await page.frames().find(f => f.name() === 'contentFrame');
    const unfoldButton = await iframe.$('#flag_ctrl');
    await unfoldButton.click();

    const LYRIC_SELECTOR = await iframe.$('#lyric-content');
    const lyricCtn = await iframe.evaluate(e => {
        return e.innerText;
    }, LYRIC_SELECTOR);

    console.log(lyricCtn);

    await page.screenshot({
        path: '歌曲.png',
        fullPage: true,
    });

    let writerStream = fs.createWriteStream('歌词.txt');
    writerStream.write(lyricCtn, 'UTF8');
    writerStream.end();

    const commentCount = await iframe.$eval('.sub.s-fc3', e => e.innerText);
    console.log(commentCount);

    // 获取评论
    const commentList = await iframe.$$eval('.itm', elements => {
        const ctn = elements.map(v => {
            return v.innerText.replace(/\s/g, ''); //把字符串所有的空格去掉。
        });
        return ctn;
    });
    console.log(commentList)
    let writerStream2 = fs.writeFileSync('评论.txt',JSON.stringify(commentList,null,'\t'));
})();
