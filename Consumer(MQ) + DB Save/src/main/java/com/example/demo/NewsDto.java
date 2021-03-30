package com.example.demo;

import lombok.Data;

import javax.persistence.*;

// Data : lombok, 자동으로 getter/setter 생성
@Data
@Entity
@Table(name = "news")
public class NewsDto {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "news_id_seq")
    @SequenceGenerator(
            name = "news_id_seq",
            sequenceName = "news_id_seq",
            allocationSize = 1
    )
    private Long id;

    // length = column data size
    @Column(length = 512)
    private String title;

    @Column(length = 65536)
    private String content;
    private String category;
}
