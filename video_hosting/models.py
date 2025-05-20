from django.db import models

# Create your models here.


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        abstract = True

class User(CommonInfo):
    id = models.PositiveIntegerField(verbose_name='Ид пользователя', primary_key=True)
    is_active = models.BooleanField(verbose_name='Активный пользователь', default=True)
    is_authenticated = models.BooleanField(verbose_name='Авторизованный пользователь', default=True)
    
    def __str__(self):
        return f'Пользователь {self.id}'
    
    class Meta:
        verbose_name = 'Пользователя хостинга'
        verbose_name_plural = 'Пользователи хостинга'


class Video(CommonInfo):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos', 
                                   verbose_name='Автор видео')
    title = models.CharField(max_length=255, verbose_name='Название видео')
    preview = models.ImageField(upload_to='videos/previews/', verbose_name='Обложка видео')
    video = models.FileField(upload_to='videos/original_files/', verbose_name='Видео', null=True, blank=True)
    duration = models.DurationField(verbose_name='Длительность видео')
    hash = models.CharField(max_length=150, verbose_name='Хеш видео', null=True, blank=True)

    processed = models.BooleanField(default=False, verbose_name='Обработано')
    hls_dir_name = models.CharField(max_length=50, verbose_name='Название директории HLS', blank=True, null=True)
    master_playlist = models.FileField(upload_to=f'videos/master_playlists/', verbose_name='Мастер плейлист', null=True)

    def __str__(self):
        return f'Видео {self.pk}, Автор {self.created_by}'
    
    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
    

class VideoTracker(CommonInfo):
    viewer = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Зритель', blank=True, null=True, related_name='watched_videos')
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='Видео', related_name='viewers')
    seconds = models.PositiveIntegerField(verbose_name='Точка просмотра видео', default=0)


    def __str__(self):
        return f'Видео {self.video_id}, Зритель {self.viewer}'
    
    class Meta:
        verbose_name = 'Просмотренное Видео'
        verbose_name_plural = 'Просмотренное Видео'


