#include "image.h"
#include "ui_image.h"
#include <QPixmap>
#include <QSize>

Image::Image(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Image)
{
    ui->setupUi(this);
}

Image::Image(QString s,QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Image)
{
    ui->setupUi(this);
    QPixmap p(s);
QSize size(ui->label->width(),ui->label->height());
p=p.scaled(size);
    ui->label->setPixmap(p);
}


Image::~Image()
{
    delete ui;
}
