// 뉴스 url : https://news.daum.net/

// 1. 다음 뉴스 홈을 요청해서 받아온다.
const request = require('request');

const cheerio = require('cheerio');

const crawlingByBreakingnews = () => {
    // digital society economic foreign culture politics
    const category = 'politics';
    
    // 적당한 day, page 값 필요
    // day 1~10 / 11~20 (size <= 10)
    // page 1~2 / 3~4 (size <= 2)
    for(let day = 11; day <= 20 ;day++) {
        for(let page = 1; page <= 2; page++) {
            
            request(`https://news.daum.net/breakingnews/${category}?page=${page}&regDate=202102${pad(day, 2)}`, (error, response, body) => {
                const $ = cheerio.load(body);
            
                let aArr = [];
                // 모든 a 태그를 긁어온다.
                aArr = $('a');

                let newsArr = [];

                // cheerio를 사용해서 attribs 사용
                // a 태그중에서 뉴스 기사만 따로 뽑아낸다.
                for(let i = 0; i < aArr.length; i++) {
                    if(aArr[i].attribs.href.includes("v.daum.net/v/"))
                    newsArr.push(aArr[i].attribs.href);
                }
            
                newsArr = Array.from(new Set(newsArr));
                
                for(let i = 0;i<newsArr.length;i++){
                    console.log(newsArr[i].split('https://v.daum.net/v/')[1]);
                    crawlingNewsByNewsTime(newsArr[i].split('https://v.daum.net/v/')[1], category);
                }
            });

            
        }
    }
    
}

const crawlingNewsByNewsTime = (newsTime, category) => {
    
    const newsUrl = `http://news.v.daum.net/v/${newsTime}`;
    
    request(newsUrl, (error, response, body) => {
        console.log(newsUrl);
        
        // request error 시 무시하고 진행.
        // 하나도 빠짐없이 가져올 필요는 없기 때문에 return 사용
        if(error !== null){
            console.log(error);
            return;
        }

        const $ = cheerio.load(body);

        let title = $('.tit_view')[0].children[0].data;
        
        let contentArr = $('#harmonyContainer p');
        let content = "";
        
        for(let i = 0 ; i<contentArr.length;i++){
            if(contentArr[i].children[0] === undefined || contentArr[i].children[0].data === undefined) {
                console.log(`[CONTINUE] contentArr[${i}].children[0].data === undefined`);
                continue;
            }
            content += contentArr[i].children[0].data + " ";
        }

        
        // Queue에 title, content, category를 전송
        let newsObject = {
            title,
            content,
            category
        }
        
        // RabbitMQ 에 메시지 전송
        globalChannel.sendToQueue(queueName, Buffer.from(JSON.stringify(newsObject)));
    });
}

let globalChannel;

const amqp = require('amqplib/callback_api');
const queueName = 'PRE_NEWS';

// RabbitMQ 연결
amqp.connect('amqp://localhost', function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel) {
        if (error1) {
            throw error1;
        }

        channel.assertQueue(queueName, {
            durable: true
        });
        globalChannel = channel;

        crawlingByBreakingnews();
    });
});

const pad = (n, width, z) => {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}