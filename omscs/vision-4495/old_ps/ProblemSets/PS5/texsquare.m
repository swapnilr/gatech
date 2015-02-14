function [i1,i2]=texSquare(isize,vx,vy,noiseLevel,textureFlag)
% a function to create two images of a textured square moving over
% a static background
% inputs: vx - the x velocity of the square
%         vy - the y velocity of the square
%         noiseLevel - the standard deviation of noise added to both frames
%         textureFlag - three possible values:
%                    1) square and background are textured
%                    2) square is textured, background isn't
%                    3) neither square nor background are textured
% outputs: i1,i2 the two frames 

i1=rand(isize);

% create square mask

[x,y]=meshgrid(1:isize);
x=x-isize/2;y=y-isize/2;
mask=abs(x)<isize/4 & abs(y)<isize/4;

if (textureFlag==2) % no background texture
 i1=i1.*mask;
elseif (textureFlag==3) % no texture at all
 i1=mask;
end

% shift the first frame according to vx,vy

x=1:isize;
x2=x-vx;% coordinates in second frame
x2=max(x2,1);x2=min(x2,isize); % make sure no coordinates are out of bounds
i1Shift=i1(:,x2);
% same for the y displacement
y=1:isize;
y2=y-vy;% coordinates in second frame
y2=max(y2,1);y2=min(y2,isize); % make sure no coordinates are out of bounds
i1Shift=i1Shift(y2,:);

% and now use mask to create i2

if (textureFlag==1)
  i2=mask.*i1Shift+(1-mask).*i1;
else
  i2=i1Shift;
end

% in the end add Gaussian noise to both frames

i1=i1+noiseLevel*randn(isize);
i2=i2+noiseLevel*randn(isize);


