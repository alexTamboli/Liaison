from django.db import models
import uuid
from users.models import Profile
from django.db.models import F
from config import Constants

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=200, blank=True, null=True)
    source_link = models.CharField(max_length=200, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key=True, editable=False)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        # ordering = ['-vote_ratio', '-vote_total', 'title']
        ordering = [
            -(F('vote_total') * Constants.PROJECT_ORDERING_RATIO[0] + F('vote_ratio') * Constants.PROJECT_ORDERING_RATIO[1]),
            'title',
        ]
        
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url
    
        
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
        
        
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()
    
    
class Review(models.Model):
    VOTE_TYPE = (
     ('up', 'Up Vote'),
     ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key=True, editable=False)
    
    class Meta:
        unique_together = [['owner', 'project']]
    
    def __str__(self) -> str:
        return self.value
    
    
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key=True, editable=False)
    
    def __str__(self) -> str:
        return self.name
    