package com.example.demo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

// JpaRepository<Entity class, ID>
// save, findOne, findAll, count, delete 등의 메소드 사용 가능.
@Repository
public interface NewsDtoRepository extends JpaRepository<NewsDto, Long> {
}
