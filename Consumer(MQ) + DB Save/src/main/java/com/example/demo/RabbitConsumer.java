package com.example.demo;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RabbitConsumer {

    // 의존성 주입
    // save, findOne, findAll, count, delete 등의 메소드 사용 가능.
    @Autowired
    NewsDtoRepository newsDtoRepository;

    // queues = "설정한 큐의 이름"
    @RabbitListener(queues = "PRE_NEWS")
    public void receiveMessage(final String message) throws JsonProcessingException {
        ObjectMapper objectMapper = new ObjectMapper();

        // readValue(읽어온 데이터, 변환할 객체 클레스)
        NewsDto newsDto = objectMapper.readValue(message, NewsDto.class);

        // DB에 데이터 저장
        newsDtoRepository.save(newsDto);
        System.out.println(newsDto);
    }
}
